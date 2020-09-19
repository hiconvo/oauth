function handleGoogleClick(googleUser) {
  const authResponse = googleUser.getAuthResponse();
  console.log(`google token: ${authResponse.id_token}`);
}

function initGoogle() {
  window.gapi.load("client", () => {
    window.gapi.client
      .init({
        apiKey: "",
        clientId: "",
        scope: "profile email",
        discoveryDocs: [
          "https://www.googleapis.com/discovery/v1/apis/people/v1/rest"
        ]
      })
      .then(() => {
        const authInstance = window.gapi.auth2.getAuthInstance();
        const googleButton = document.getElementById("google");
        authInstance.attachClickHandler(
          googleButton,
          {},
          handleGoogleClick,
          e => {
            alert(e);
          }
        );
      });
  });
}

document.addEventListener("DOMContentLoaded", initGoogle);
