// Generate participant ID at the start
let participant_id = `participant${Math.floor(Math.random() * 999) + 1}`;

var jsPsych = initJsPsych();

var filename = jsPsych.randomization.randomID(10) + ".csv";
var timeline = [];
    
    //var preload = {
        //type: jsPsychPreload,
        //video: ['stimuli/norming/batent1.mp4'],
    //};
    //timeline.push(preload);


var instructions = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
        <p>In this experiment, you will see a video and will be asked to describe what is happening</p>
        <p>Press any key to begin.</p>
        `,
    };

    // trials = generate_trials.py //array of random order from generate_trials
    /** for (let i =0; i < trials.length; i++) {
        var trial = {
            type: jsPsychVideoKeyboardResponse,
            stimulus: [trails[i]],
            choices: ['enter'],
            prompt: "<p>Describe what you see in the video.</p>",
        };
        timeline.push(trial);
    }
        */

    // working example
var trial = {
    type: jsPsychVideoKeyboardResponse,
    stimulus: ['stimuli/norming/batent1.mp4'],
    choices: ['enter'],
    prompt: "<p>Describe what you see in the video.</p>",
    height: 480,
    width: 480,
    data: {
        video_id: 'batent1',
    }

};

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

// Function to load trials
async function loadTrials() {
    try {
        // Determine which file to load
        let filename = 'trials.csv'; // default file
        
        const response = await fetch(filename);
        const csvText = await response.text();
        
        const results = Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            dynamicTyping: true
        });

        // Log the first trial to check structure
        console.log('Sample trial structure:', results.data[0]);

        // Shuffle the trials
        let shuffledData = [...results.data];
        for (let i = shuffledData.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffledData[i], shuffledData[j]] = [shuffledData[j], shuffledData[i]];
        }
        
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
    
const save_data = {
    type: jsPsychPipe,
    action: "save",
    experiment_id: "DvojIUx5ETI3",
    filename: filename,
    data_string: ()=>jsPsych.data.get().csv()
};

function getVideoPath(stimName) {
    return `stimuli/norming/${stimName}.mp4`;
}

// Function to create trials
function createTrials(trialsData) {
    let allTrials = [];
    
    trialsData.forEach(trial => {

        // Second part: Show both top stimulus and shuffled choice buttons
        const responseTrial = {
            type: jsPsychVideoKeyboardResponse,
            stimulus: getVideoPath(trial.filename),
            stimulus_height: 200,
            maintain_aspect_ratio: true,
            choices: choiceStims.map(stim => {
                const videoPath = getImagePath(stim.stim);
                console.log('Loading choice stimulus:', videoPath);
                return '<img src="' + videoPath + '" style="max-width:200px; max-height:200px;">';
            }),
            response_ends_trial: true,
            post_trial_gap: 500,
            data: {
                subCode: participant_id
            },
            on_finish: function(data) {
                data.rt = Math.round(data.rt);
                data.trial_part = 'critical_trial';
            }
        };

        allTrials.push(topStimTrial, choiceTrial);
    });
    
    return allTrials;
}

async function runExperiment() {
    try {
        // Load trials
        const trialsData = await loadTrials();
        console.log('Loaded trials:', trialsData.length);
        
        if (trialsData.length === 0) {
            console.error('No trials loaded!');
            return;
        }

        // Create timeline
        const timeline = [
            consent,
            instructions,
            ...createTrials(trialsData),
            save_data
        ];

        // Run the experiment
        await jsPsych.run(timeline);
    } catch (error) {
        console.error('Error running experiment:', error);
    }
}

      


// Start the experiment when the page loads
runExperiment();