

var jsPsych = initJsPsych();

    var filename = jsPsych.randomization.randomID(10) + ".csv";
    var timeline = [];
    
    var preload = {
        type: jsPsychPreload,
        video: ['stimuli/norming/batent1.mp4'],
    };
    timeline.push(preload);

    var welcome = {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: "Welcome to the experiment. Press any key to begin."
    };
    timeline.push(welcome);

    var instructions = {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: `
            <p>In this experiment, you will see a video and will be asked to describe what is happening</p>
            <p>Press any key to begin.</p>
        `,
    };
    timeline.push(instructions);

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
    timeline.push(trial);

    var end = {
      type: jsPsychHtmlKeyboardResponse,
      stimulus: "Thank you for participating! Press any key to finish."
    }
    timeline.push(end);
    
    const save_data = {
        type: jsPsychPipe,
        action: "save",
        experiment_id: "DvojIUx5ETI3",
        filename: filename,
        data_string: ()=>jsPsych.data.get().csv()
      };

    jsPsych.run(timeline);