document.getElementById("upload-form").addEventListener("submit", function(event) {
   event.preventDefault();

   const fileSupplied = document.getElementById('file-note');
   if (!fileSupplied.files.length) {
      event.preventDefault();
      showToast('Please upload a file first.');
      return;
   } else {
      setTimeout(function() {
         event.target.submit();
      }, 1);
   }
});

function showToast(message) {
   const toast = document.createElement('div');
   toast.className = 'fixed bottom-4 left-4 bg-blue-500 text-white p-4 rounded-2xl shadow-lg';
   toast.style.opacity = 0;
   toast.style.transition = 'opacity 0.2s';
   toast.innerHTML = message;
   document.body.appendChild(toast);
   
   setTimeout(() => {
      toast.style.opacity = 1;
   }, 100);

   setTimeout(() => {
      toast.style.opacity = 0;
      setTimeout(() => {
         document.body.removeChild(toast);
      }, 200);
   }, 3000);
}

document.getElementById('question').addEventListener('keydown', function(event) {
   if (event.key === 'Enter') {
      event.preventDefault();
      document.getElementById('ask-question').click();
   }
});

document.getElementById('ask-question').addEventListener('click', async function() {

   const noteId = document.getElementById('note-selection').value;
   const question = document.getElementById('question').value;
   const askButton = document.getElementById('ask-question');
   const answerDiv = document.getElementById('answer');

   if (!noteId) {
      showToast('Please select a note first.');
      return;
   }

   if (noteId && question) {
      // Display spinner and change button text
      askButton.innerHTML = 'Processing...';
      askButton.disabled = true;
      answerDiv.innerHTML = '<div class="spinner-notes"></div>';

      const response = await fetch('/ask_note', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            note_id: noteId,
            question: question
         })
      });

      const data = await response.json();
      document.getElementById('answer').innerHTML = `<p><strong>Answer:</strong> ${data.answer}</p>`;

      // Hide spinner and restore button text
      askButton.innerHTML = 'Ask';
      askButton.disabled = false;
   }
});