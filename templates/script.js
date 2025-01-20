// script.js

document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Gather form data
    const userEmail = document.getElementById("email").value;
    const userMessage = document.getElementById("message").value;

    // Send data to Flask backend
    fetch('https://get-to-know-me.onrender.com/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: userEmail,
            message: userMessage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle success (e.g., show a thank you message)
        alert("Message sent successfully!");
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error (e.g., show an error message)
        alert("Failed to send your message. Please try again.");
    });
});
