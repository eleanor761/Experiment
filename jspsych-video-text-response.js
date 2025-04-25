/**
 * jspsych-video-text-response
 * A jsPsych plugin for displaying a video stimulus and collecting a text response
 */
var jsPsychVideoTextResponse = (function (jspsych) {
  'use strict';

  const info = {
    name: 'video-text-response',
    parameters: {
      /** 
       * The video file to play. Video can be provided in multiple file formats.
       */
      stimulus: {
        type: jspsych.ParameterType.VIDEO,
        pretty_name: 'Video',
        default: undefined,
        description: 'Video files to be played.'
      },
      /** Width of the video in pixels */
      width: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Width',
        default: 640,
        description: 'The width of the video in pixels.'
      },
      /** Height of the video in pixels */
      height: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Height',
        default: 360,
        description: 'The height of the video in pixels.'
      },
      /** Whether to autoplay the video */
      autoplay: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: 'Autoplay',
        default: true,
        description: 'If true, the video will autoplay.'
      },
      /** Whether to loop the video */
      loop: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: 'Loop',
        default: false,
        description: 'If true, the video will loop.'
      },
      /** Whether to show video controls */
      controls: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: 'Controls',
        default: false,
        description: 'If true, video controls will be available.'
      },
      /** Prompt to display above the video */
      prompt: {
        type: jspsych.ParameterType.HTML_STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed above the video.'
      },
      /** Label to display for the text input */
      question_text: {
        type: jspsych.ParameterType.HTML_STRING,
        pretty_name: 'Question Text',
        default: 'Please provide your response:',
        description: 'Text to display above the text input.'
      },
      /** Placeholder text for the response text box */
      placeholder: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Placeholder',
        default: '',
        description: 'Placeholder text for the text box.'
      },
      /** The number of rows for the response text box */
      rows: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Rows',
        default: 5,
        description: 'The number of rows for the response text box.'
      },
      /** The number of columns for the response text box */
      columns: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Columns',
        default: 40,
        description: 'The number of columns for the response text box.'
      },
      /** Whether or not to show the text input before the video finishes */
      show_response_during_video: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: 'Show Response During Video',
        default: true,
        description: 'If true, response area appears during the video.'
      },
      /** Label for the continue button */
      button_label: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Button label',
        default: 'Continue',
        description: 'Label of the button to finish the trial.'
      },
      /** Whether to require a response */
      required: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: 'Required',
        default: false,
        description: 'Whether or not a response is required'
      },
      /** Time to wait after the video ends before enabling response */
      time_after_video: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Time After Video',
        default: 0,
        description: 'Time to wait after the video finishes before showing/enabling response (ms)'
      }
    }
  };

  /**
   * **video-text-response**
   * 
   * A plugin for displaying a video stimulus and collecting a text response
   */
  class VideoTextResponsePlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
      console.log('Starting video-text-response trial');
      
      // Display the video stimulus
      let html = '<div id="jspsych-video-text-response-wrapper" style="margin: 0 auto;">';
      
      // Skip the Video X title prompt
      if (trial.prompt !== null && !trial.prompt.includes('Video')) {
        html += `<div id="jspsych-video-text-response-prompt">${trial.prompt}</div>`;
      }

      // Display the video
      html += '<div id="jspsych-video-text-response-stimulus">';
      html += '<video controls muted id="jspsych-video-text-response-video" width="' + trial.width + '" height="' + trial.height + '"';
      
      if(trial.autoplay){
        html += " autoplay";
      }
      if(trial.loop){
        html += " loop";
      }
      if(trial.controls){
        html += " controls";
      }
      html += ">";
      
      var video_preload_blob = this.jsPsych.pluginAPI.getVideoBuffer(trial.stimulus[0]);
      if (!video_preload_blob) {
        for (var i = 0; i < trial.stimulus.length; i++) {
          var file_name = trial.stimulus[i];
          if (file_name.indexOf('?') > -1) {
            file_name = file_name.substring(0, file_name.indexOf('?'));
          }
          var type = file_name.substr(file_name.lastIndexOf('.') + 1);
          type = type.toLowerCase();
          if (type == 'mov') {
            console.warn('Warning: video-text-response plugin does not reliably support .mov files.');
            type = 'mp4';
          } else if (type == 'mpeg') {
            type = 'mp4';
          }
          html += '<source src="' + file_name + '" type="video/' + type + '">';
        }
      }
      html += "</video>";
      html += "</div>";
      
      // Add response elements
      html += '<div id="jspsych-video-text-response-response-area">';
      
      // Add question text
      html += `<p class="jspsych-video-text-response-question">${trial.question_text}</p>`;
      
      // Add text area
      html += '<textarea name="response" id="jspsych-video-text-response-text" cols="' + 
        trial.columns + '" rows="' + trial.rows + '" placeholder="' + 
        trial.placeholder + '"></textarea>';
      
      // Add submit button - always disabled initially
      html += '<button id="jspsych-video-text-response-next" class="jspsych-btn" disabled>' + 
        trial.button_label + '</button>';
      
      html += '</div>';
      html += '</div>';
      
      display_element.innerHTML = html;
      
      // Get video element after adding to DOM
      const video_element = display_element.querySelector('#jspsych-video-text-response-video');
      const textArea = display_element.querySelector('#jspsych-video-text-response-text');
      const submitButton = display_element.querySelector('#jspsych-video-text-response-next');
      
      console.log('DOM elements setup complete');
      
      // Set up video preload
      if (video_preload_blob) {
        video_element.src = video_preload_blob;
      }
      
      // Variables to track state
      let videoCompleted = false;
      let videoDuration = 0;
      let videoPlayedOnce = false;
      let self = this; // Store this reference for callbacks
      
      // Function to check if button should be enabled
      function checkEnableButton() {
        // For required responses, need both video completion and text
        if (trial.required) {
          submitButton.disabled = !(videoPlayedOnce && textArea.value.trim() !== '');
        } else {
          // If not required, just need video completion
          submitButton.disabled = !videoPlayedOnce;
        }
        
        console.log('Button state check: videoPlayedOnce =', videoPlayedOnce, 
                   'text =', textArea.value.trim(), 
                   'button disabled =', submitButton.disabled);
      }
      
      // Get video duration when metadata is loaded
      video_element.addEventListener('loadedmetadata', function() {
        videoDuration = video_element.duration;
        console.log('Video duration:', videoDuration);
      });
      
      // Track video progress to detect first complete play
      video_element.addEventListener('timeupdate', function() {
        // If we're near the end of the video and haven't marked it as played once
        if (!videoPlayedOnce && video_element.currentTime > 0 && 
            videoDuration > 0 && videoDuration - video_element.currentTime < 0.5) {
          console.log('Video has played through once');
          videoPlayedOnce = true;
          checkEnableButton();
        }
      });
      
      // Also handle ended event (for non-looping videos)
      video_element.addEventListener('ended', function() {
        console.log('Video ended event fired');
        videoPlayedOnce = true;
        checkEnableButton();
      });
      
      // Listen for text input changes
      textArea.addEventListener('input', function() {
        console.log('Text input changed: ', textArea.value);
        checkEnableButton();
      });
      
      // Function to end trial
      function end_trial() {
        console.log('End trial called');
        
        const trial_data = {
          rt: performance.now() - start_time,
          stimulus: trial.stimulus,
          response: textArea.value,
          response_text: textArea.value,
          trial_type: 'video-text-response'
        };
        
        display_element.innerHTML = '';
        self.jsPsych.finishTrial(trial_data);
      }
      
      // Handle button click
      submitButton.addEventListener('click', end_trial);
      
      // Start timing
      var start_time = performance.now();
      console.log('Trial started at:', start_time);
    }
  }

  VideoTextResponsePlugin.info = info;

  return VideoTextResponsePlugin;
})(jsPsychModule);

// This makes the plugin accessible to the experiment in jsPsych 7.x
if (typeof jsPsychModule !== 'undefined') {
  jsPsychModule.VideoTextResponsePlugin = jsPsychVideoTextResponse;
}