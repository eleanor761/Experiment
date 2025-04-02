// Generate participant ID at the start
let participant_id = `participant${Math.floor(Math.random() * 999) + 1}`;

// Initialize jsPsych
const jsPsych = new jsPsychModule.JsPsych({
  show_progress_bar: true,
  auto_update_progress_bar: false
});

// Create a random filename for data saving
const filename = jsPsych.randomization.randomID(10) + ".csv";
let timeline = [];

// Define the consent form 
const consent = {
    type: jsPsychHtmlButtonResponse,  
    stimulus: `
        <div style="width: 800px; margin: 0 auto; text-align: left">
            <h3>Consent to Participate in Research</h3>
            
            <p>The task you are about to do is sponsored by University of Wisconsin-Madison. It is part of a protocol titled "What are we learning from language?"</p>

            <p>The task you are asked to do involves making simple responses to words and sentences. For example, you may be asked to rate a pair of words on their similarity or to indicate how true you think a given sentence is. More detailed instructions for this specific task will be provided on the next screen.</p>

            <p>This task has no direct benefits. We do not anticipate any psychosocial risks. There is a risk of a confidentiality breach. Participants may become fatigued or frustrated due to the length of the study.</p>

            <p>The responses you submit as part of this task will be stored on a sercure server and accessible only to researchers who have been approved by UW-Madison. Processed data with all identifiers removed could be used for future research studies or distributed to another investigator for future research studies without additional informed consent from the subject or the legally authorized representative.</p>

            <p>You are free to decline to participate, to end participation at any time for any reason, or to refuse to answer any individual question without penalty or loss of earned compensation. We will not retain data from partial responses. If you would like to withdraw your data after participating, you may send an email lupyan@wisc.edu or complete this form which will allow you to make a request anonymously.</p>

            <p>If you have any questions or concerns about this task please contact the principal investigator: Prof. Gary Lupyan at lupyan@wisc.edu.</p>

            <p>If you are not satisfied with response of the research team, have more questions, or want to talk with someone about your rights as a research participant, you should contact University of Wisconsin's Education Research and Social & Behavioral Science IRB Office at 608-263-2320.</p>

            <p><strong>By clicking the box below, I consent to participate in this task and affirm that I am at least 18 years old.</strong></p>
        </div>
    `,
    choices: ['I Agree', 'I Do Not Agree'],
    data: {
        trial_type: 'consent'
    },
    on_finish: function(data) {
        if(data.response == 1) {
            jsPsych.endExperiment('Thank you for your time. The experiment has been ended.');
        }
    }
};

// Instructions block
const instructions = {
    type: jsPsychHtmlKeyboardResponse,  
    stimulus: `
        <p>In this experiment, you will see a video and will be asked to describe what is happening</p>
        <p>Press any key to begin.</p>
    `,
};

// Text response after video
const responseTextTrial = {
    type: jsPsychSurveyText,
    questions: [
        {
            prompt: 'Please describe what you saw in the video:', 
            required: true,
            rows: 5,
            columns: 60
        }
    ],
    data: {
        trial_type: 'response',
        video_id: 'batent1',
        subCode: participant_id
    }
};

// Function to get video path from filename
function getVideoPath(stimName) {
    return `stimuli/norming/${stimName}`;
}

function createTrials(trialsData) {
    const experimentTrials = [];
    
    trialsData.forEach(trial => {
        // Try different possible field names for the filename
        const videoFile = trial.filename || trial.file_name || trial.video || trial.stimuli;
        
        if (!videoFile) {
            console.warn('Trial missing filename field:', trial);
            return;
        }
        
        // Create combined video and text response trial
        const combinedTrial = {
            type: jsPsychHtmlButtonResponse,
            stimulus: function() {
                const videoPath = getVideoPath(videoFile);
                return `
                    <div style="display: flex; flex-direction: column; align-items: center;">
                        <video id="jspsych-video" width="640" height="480" controls autoplay loop>
                            <source src="${videoPath}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <div style="margin-top: 20px; width: 80%;">
                            <p><strong>Please describe what you see in the video:</strong></p>
                            <textarea id="response-text" rows="5" style="width: 100%; padding: 10px;"></textarea>
                        </div>
                    </div>
                `;
            },
            choices: ['Submit'],
            data: {
                video_id: videoFile,
                trial_num: trial.trial_num,
                type: trial.type || 'unknown',
                subCode: participant_id,
                trial_type: 'video_with_response'
            },
            on_finish: function(data) {
                // Get the text response and save it
                const responseText = document.getElementById('response-text').value;
                data.response_text = responseText;
            }
        };

        experimentTrials.push(combinedTrial);
    });
    
    return experimentTrials;
}


// Preload media files
const preload = {
    type: jsPsychPreload, 
    auto_preload: true
};

// Data saving configuration
const save_data = {
    type: jsPsychPipe, 
    action: "save",
    experiment_id: "DvojIUx5ETI3",
    filename: filename,
    data_string: () => jsPsych.data.get().csv()
};

// Function to load trials from CSV
async function loadTrials() {
    try {
        const csvFilename = 'demo_trials.csv'; // Path to your trials file, will need to udpate once all videos are done
        
        const response = await fetch(csvFilename);
        const csvText = await response.text();
        
        const results = Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            dynamicTyping: true
        });

        console.log('Sample trial structure:', results.data[0]);

        // Shuffle the trials
        let shuffledData = jsPsych.randomization.shuffle([...results.data]);
        
        // Update trial numbers to match new order
        shuffledData = shuffledData.map((trial, index) => ({
            ...trial,
            trial_num: index
        }));
        
        return shuffledData;
    } catch (error) {
        console.error('Error loading trials:', error);
        return [];
    }
}

// Main function to run the experiment
async function runExperiment() {
    try {
        // Load trials
        const trialsData = await loadTrials();
        console.log('Loaded trials:', trialsData.length);
        

        // Create full timeline with loaded trials
        const experimentTrials = createTrials(trialsData);
            
        timeline = [
            consent,
            instructions,
            preload,
            ...experimentTrials,
            save_data
            ];

        // Run the experiment
        jsPsych.run(timeline);
    } catch (error) {
        console.error('Error running experiment:', error);
        // Display error message on the page
        document.getElementById('jspsych-target').innerHTML = `
            <div style="max-width: 800px; margin: 50px auto; padding: 20px; background: #f8f8f8; border-radius: 5px;">
                <h2>Error Starting Experiment</h2>
                <p>There was a problem starting the experiment. Please try refreshing the page.</p>
                <p>If the problem persists, please contact the researcher.</p>
                <p>Technical details: ${error.message}</p>
            </div>
        `;
    }
}

// Wait for the page to load before starting the experiment
document.addEventListener('DOMContentLoaded', runExperiment);