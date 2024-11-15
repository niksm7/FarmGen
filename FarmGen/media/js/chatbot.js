document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");
  
    sendBtn.addEventListener("click", async () => {
      const userMessage = userInput.value.trim();
      if (!userMessage) return;
  
      // Add user message to chat
      addMessageToChat("user-message", userMessage);
  
      // Display "typing..." message
      const typingIndicator = addMessageToChat("bot-message", "Typing...");

      // Clear the input
      userInput.value = "";
  
      // Send request to Django API
      const response = await fetchDjangoApi(userMessage);
  
      // Remove "typing..." message and display the actual response
      typingIndicator.remove();
      addMessageToChat("bot-message", response);
  
    });
  
    async function fetchDjangoApi(message) {
      try {
        const response = await fetch("/getchatbotresponse/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: message }),
        });
  
        if (response.ok) {
          const data = await response.json();
          return data.response;
        } else {
          console.error("Error from server", response.statusText);
          return "Something went wrong, please try again.";
        }
      } catch (error) {
        console.error("Error:", error);
        return "Error connecting to the server.";
      }
    }
  
    function addMessageToChat(className, message) {
      const messageElement = document.createElement("div");
      messageElement.className = className;
      messageElement.textContent = message;
      chatBox.appendChild(messageElement);
      chatBox.scrollTop = chatBox.scrollHeight;
      return messageElement;
    }
  });
  