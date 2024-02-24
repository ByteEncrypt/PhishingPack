const form = document.getElementById("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(document.getElementById("form"));

  const user_agent = navigator.userAgent;
  const date = new Date();
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
    hour: "numeric",
    minute: "numeric",
  };
  const time = date.toLocaleString("en-US", options);

  formData.append("user_agent", user_agent);
  formData.append("time", time);

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/submit", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      window.location.replace(xhr.responseText);
    }
  };
  xhr.send(formData);
});
