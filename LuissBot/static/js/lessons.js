document.getElementById('file-input').addEventListener('change', function (event) {
   var fileNameElement = document.getElementById('file-name');
   if (event.target.files.length > 0) {
       fileNameElement.textContent = event.target.files[0].name;
   } else {
       fileNameElement.textContent = "";
   }
});

function displayToast(message) {
   const toast = document.getElementById('toast');
   toast.textContent = message;
   toast.classList.add('show');
   setTimeout(function() {
       toast.classList.remove('show');
   }, 3000);
}


document.getElementById("transcription-form").addEventListener("submit", function(event) {

   const fileSupplied = document.getElementById('file-input');
   if (!fileSupplied.files.length) {
      event.preventDefault();
      displayToast('Please upload a file first.');
      return;
   } else {

      var submitButton = event.target.querySelector('button[type="submit"]');
      var transcribeText = document.getElementById("transcribe-text");
      var transcribeSpinner = document.getElementById("transcribe-spinner");
      var fileInput = document.getElementById("file-input");
      var estimatedTimeElement = document.getElementById("estimated-time");
   
      // Show the loading animation and change the button text
      transcribeText.textContent = "Transcribing...";
      transcribeSpinner.style.display = "inline-block";
      submitButton.disabled = true;

      // Function to format the estimated time
      function formatTime(minutes, seconds) {
         return "Estimated time: " +
            (minutes < 10 ? "0" + minutes : minutes) + " min " +
            (seconds < 10 ? "0" + seconds : seconds) + " sec";
      }

      // Calculate estimated time based on the audio duration
      if (fileInput.files.length > 0) {
         var file = fileInput.files[0];
         var audioElement = new Audio(URL.createObjectURL(file));
         audioElement.addEventListener("loadedmetadata", function() {
            var duration = audioElement.duration;
            var transcriptionSpeed = 0.1269; // Adjust this value based on actual transcription speed
            var estimatedTime = Math.ceil(duration * transcriptionSpeed);
            var minutes = Math.floor(estimatedTime / 60);
            var seconds = estimatedTime % 60;
            estimatedTimeElement.textContent = formatTime(minutes, seconds);
         });
      }
   
      // Submit the form after a short delay to allow the UI to update
      setTimeout(function() {
         event.target.submit();
      }, 100);
      
   }
});

document.getElementById('query').addEventListener('keydown', function(event) {
   if (event.key === 'Enter') {
      event.preventDefault();
      document.getElementById('ask-query').click();
   }
});

document.getElementById('ask-query').addEventListener('click', async function() {

   const question = document.getElementById('query').value;
   const askButton = document.getElementById('ask-query');
   const answerDiv = document.getElementById('form-answer');

   if (question) {
      // Display spinner and change button text
      askButton.innerHTML = 'Processing...';
      askButton.disabled = true;
      answerDiv.innerHTML = '<div class="spinner-notes"></div>';

      const response = await fetch('/ask_question', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            question: question
         })
      });

      const data = await response.json();
      document.getElementById('form-answer').innerHTML = `<p><strong>Answer:</strong> ${data.answer}</p>`;

      // Hide spinner and restore button text
      askButton.innerHTML = 'Ask';
      askButton.disabled = false;
   }
});