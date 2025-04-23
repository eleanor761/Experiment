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
      // Display the video stimulus
      let html = '<div id="jspsych-video-text-response-wrapper" style="margin: 0 auto;">';
      
      // Add prompt if there is one
      if (trial.prompt !== null) {
        html += `<div id="jspsych-video-text-response-prompt">${trial.prompt}</div>`;
      }
  
      // Display the video
      html += '<div id="jspsych-video-text-response-stimulus">';
      html += '<video id="jspsych-video-text-response-video" width="' + trial.width + '" height="' + trial.height + '"';
      
      if(trial.autoplay){
        html += " autoplay muted ";
      }
      if(trial.loop){
        html += " loop ";
      }
      if(trial.controls){
        html += " controls ";
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
      html += '<div id="jspsych-video-text-response-response-area"';
      if (!trial.show_response_during_video) {
        html += ' style="display:none;"';
      }
      html += '>';
      
      // Add question text
      html += `<p class="jspsych-video-text-response-question">${trial.question_text}</p>`;
      
      // Add text area
      html += '<textarea name="response" id="jspsych-video-text-response-text" cols="' + 
        trial.columns + '" rows="' + trial.rows + '" placeholder="' + 
        trial.placeholder + '"';
      
      if (trial.required && !trial.show_response_during_video) {
        html += ' required';
      }
      
      html += '></textarea>';
      
      // Add submit button
      html += '<button id="jspsych-video-text-response-next" class="jspsych-btn"';
      if (trial.required) {
        html += ' disabled';
      }
      html += '>' + trial.button_label + '</button>';
      
      html += '</div>';
      html += '</div>';
      
      display_element.innerHTML = html;
      
      // Now get video element AFTER adding to DOM
      const video_element = display_element.querySelector('#jspsych-video-text-response-video');
      
      // Video playback tracking
      let videoPlayed = false;
      
      // Set up video preload
      if (video_preload_blob) {
        video_element.src = video_preload_blob;
      }
      
      // Response validation logic
      if (trial.required) {
        const textArea = document.getElementById('jspsych-video-text-response-text');
        const nextButton = document.getElementById('jspsych-video-text-response-next');
        
        // Function to check if response is valid
        const checkResponseValid = function() {
          // If video must be watched and hasn't been, keep button disabled
          if (!trial.show_response_during_video && !videoPlayed) {
            nextButton.disabled = true;
            return;
          }
          
          // Enable button only if there's text
          nextButton.disabled = textArea.value.trim() === '';
        };
        
        // Check validity whenever text changes
        textArea.addEventListener('input', checkResponseValid);
        
        // Also check validity when video ends
        video_element.addEventListener('ended', function() {
          videoPlayed = true;
          
          // Show response area if it was hidden
          if (!trial.show_response_during_video) {
            setTimeout(() => {
              document.getElementById('jspsych-video-text-response-response-area').style.display = 'block';
              checkResponseValid();
            }, trial.time_after_video);
          } else {
            checkResponseValid();
          }
        });
        
        // Also handle timeupdate event for partial video watching
        video_element.addEventListener('timeupdate', function() {
          // If we've played at least 2 seconds and haven't already marked as played
          if (video_element.currentTime > 2 && !videoPlayed) {
            videoPlayed = true;
            checkResponseValid();
          }
        });
      } else {
        // If response not required, just handle video end
        video_element.addEventListener('ended', function() {
          videoPlayed = true;
          
          // Show response area if it was hidden
          if (!trial.show_response_during_video) {
            setTimeout(() => {
              document.getElementById('jspsych-video-text-response-response-area').style.display = 'block';
            }, trial.time_after_video);
          }
          
          // Enable button
          document.getElementById('jspsych-video-text-response-next').disabled = false;
        });
        
        // If showing during video and not required, enable button immediately
        if (trial.show_response_during_video) {
          document.getElementById('jspsych-video-text-response-next').disabled = false;
        }
      }
      
      let trial_complete = false;
      
      // Function to end trial
      const end_trial = () => {
        // Only execute if trial not already complete
        if (trial_complete) return;
        trial_complete = true;
        
        // Gather data
        const trial_data = {
          rt: performance.now() - start_time,
          stimulus: trial.stimulus,
          response: display_element.querySelector('#jspsych-video-text-response-text').value,
          trial_type: 'video-text-response'
        };
        
        // Clear display
        display_element.innerHTML = '';
        
        // End trial
        this.jsPsych.finishTrial(trial_data);
      };
      
      // Handle button click
      display_element.querySelector('#jspsych-video-text-response-next').addEventListener('click', end_trial);
      
      // Start timing
      var start_time = performance.now();
    }
  }
  
  VideoTextResponsePlugin.info = info;
  
  return VideoTextResponsePlugin;
  })(jsPsychModule);
  
  // This makes the plugin accessible to the experiment
  if (typeof jsPsychModule !== 'undefined') {
    var jsPsychVideoTextResponse = jsPsychModule.registerPlugin('video-text-response', VideoTextResponsePlugin);
  }