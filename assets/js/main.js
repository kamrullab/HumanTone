document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       COPY PROMPT BUTTON
    ========================== */
  
    const promptContent = document.querySelector(".prompt-content");
  
    if (promptContent) {
      const copyButton = document.createElement("button");
  
      copyButton.className = "copy-prompt-button";
      copyButton.textContent = "Copy Prompt";
  
      promptContent.parentNode.insertBefore(
        copyButton,
        promptContent
      );
  
      copyButton.addEventListener("click", async () => {
        const text = promptContent.innerText;
  
        try {
          await navigator.clipboard.writeText(text);
  
          copyButton.textContent = "Copied!";
  
          setTimeout(() => {
            copyButton.textContent = "Copy Prompt";
          }, 2000);
  
        } catch (error) {
          copyButton.textContent = "Copy failed";
  
          setTimeout(() => {
            copyButton.textContent = "Copy Prompt";
          }, 2000);
        }
      });
    }
  
  
    /* =========================
       ACTIVE NAVIGATION
    ========================== */
  
    const currentPath = window.location.pathname;
  
    const navLinks = document.querySelectorAll(".nav-links a");
  
    navLinks.forEach((link) => {
      const linkUrl = new URL(
        link.href,
        window.location.origin
      );
  
      if (
        linkUrl.pathname === currentPath &&
        linkUrl.hash === ""
      ) {
        link.classList.add("active");
      }
    });
  
  });