document.addEventListener("DOMContentLoaded", function() {
    // Create the modal container element
    const modal = document.createElement("div");
    modal.id = "myModal";
    modal.className = "modal";
  
    // Create the modal content element
    const modalContent = document.createElement("div");
    modalContent.className = "modal-content";
  
    // Create the close button
    const closeBtn = document.createElement("span");
    closeBtn.className = "close";
    closeBtn.innerHTML = "&times;"; // HTML for the "x" symbol
  
    // Create the content paragraph
    const contentPara = document.createElement("p");
    contentPara.textContent = "This is your onload pop-up!";
  
    // Assemble the modal content
    modalContent.appendChild(closeBtn);
    modalContent.appendChild(contentPara);
    modal.appendChild(modalContent);
  
    // Append the modal to the body so it exists on the page
    document.body.appendChild(modal);
  
    // Create and inject the CSS styles for the modal into the head
    const style = document.createElement("style");
    style.textContent = `
      /* Modal container - hidden by default */
      .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.5); /* Black overlay with opacity */
      }
      /* Modal content box */
      .modal-content {
        background-color: #fff;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
        max-width: 500px;
      }
      /* Close button styling */
      .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
      }
      .close:hover {
        color: #000;
      }
    `;
    document.head.appendChild(style);
  
    // Show the modal as soon as the page loads
    modal.style.display = "block";
  
    // Close the modal when the close button is clicked
    closeBtn.addEventListener("click", function() {
      modal.style.display = "none";
    });
  
    // Optionally close the modal when clicking outside of the modal content
    window.addEventListener("click", function(event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
  });
  