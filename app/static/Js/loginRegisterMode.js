const container = document.querySelector(".container");
const registerBtn = document.querySelector(".register-btn");
const loginBtn = document.querySelector(".login-btn");

// Hàm xóa flash messages
function removeFlashMessages() {
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((msg) => {
    msg.remove();
  });
}

// Khởi tạo theo tham số URL: ?mode=register hoặc hash #register
document.addEventListener("DOMContentLoaded", () => {
  if (!container) return;
  const params = new URLSearchParams(window.location.search);
  const mode = params.get("mode") || window.location.hash.replace("#", "");
  if (mode && mode.toLowerCase() === "register") {
    container.classList.add("active");
  } else if (mode && mode.toLowerCase() === "login") {
    container.classList.remove("active");
  }

  // Tự động xóa flash messages sau 5 giây
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((msg) => {
    setTimeout(() => {
      msg.style.transition = "opacity 0.5s";
      msg.style.opacity = "0";
      setTimeout(() => {
        msg.remove();
      }, 500);
    }, 5000);
  });
});

if (registerBtn) {
  registerBtn.addEventListener("click", (e) => {
    e.preventDefault();
    removeFlashMessages(); // Xóa flash messages khi chuyển form
    container.classList.add("active");
    // Cập nhật URL với mode=register
    const url = new URL(window.location);
    url.searchParams.set("mode", "register");
    window.history.pushState({}, "", url);
  });
}

if (loginBtn) {
  loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    removeFlashMessages(); // Xóa flash messages khi chuyển form
    container.classList.remove("active");
    // Cập nhật URL với mode=login
    const url = new URL(window.location);
    url.searchParams.set("mode", "login");
    window.history.pushState({}, "", url);
  });
}

// Xóa flash messages khi reload trang nếu không có trong URL (tránh hiển thị lại)
window.addEventListener("beforeunload", () => {
  // Flash messages sẽ tự động bị xóa bởi Flask sau khi được đọc
  // Nhưng để chắc chắn, ta có thể xóa bằng JS
  removeFlashMessages();
});
