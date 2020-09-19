function handleFBClick(e) {
  e.preventDefault();
  window.FB.login(
    response => {
      console.log(`facebook token: ${response.authResponse.accessToken}`);
    },
    { scope: "public_profile,email" }
  );
}

function initFB() {
  window.FB.init({
    appId: "406328056661427",
    autoLogAppEvents: true,
    xfbml: true,
    version: "v3.3"
  });
}

document.addEventListener("DOMContentLoaded", initFB);
document.getElementById("facebook").addEventListener("click", handleFBClick);
