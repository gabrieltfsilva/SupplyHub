function togglePw(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  if (input.type === "password") {
    input.type = "text";
    icon.className = "bi bi-eye-slash";
  } else {
    input.type = "password";
    icon.className = "bi bi-eye";
  }
}

function checkMatch() {
  const s1 = document.getElementById("password1").value;
  const s2 = document.getElementById("password2");
  const msg = document.getElementById("match-msg");

  if (!s2.value) {
    s2.classList.remove("match-ok", "match-err");
    msg.style.display = "none";
    return;
  }

  if (s1 === s2.value) {
    s2.classList.add("match-ok");
    s2.classList.remove("match-err");
    msg.style.display = "block";
    msg.style.color = "#1db954";
    msg.textContent = "✓ Senhas coincidem";
  } else {
    s2.classList.add("match-err");
    s2.classList.remove("match-ok");
    msg.style.display = "block";
    msg.style.color = "#e5341d";
    msg.textContent = "✗ Senhas não coincidem";
  }
}
