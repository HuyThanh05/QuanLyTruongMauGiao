const studentsPerPage = 15;
let currentPage = 1;
let data = [];
let totalPages = 1;

async function fetchStudents() {
  const student_list = document.getElementById("student_list");
  if (!student_list) return;

  // Hiển thị loading
  student_list.innerHTML =
    '<tr><td colspan="7" class="text-center"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div> Đang tải dữ liệu...</td></tr>';

  try {
    // Lấy query parameter từ URL nếu có
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("q") || "";

    const apiUrl = `/api/students${
      query ? `?q=${encodeURIComponent(query)}` : ""
    }`;
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error("Failed to fetch students");
    }

    data = await response.json();
    totalPages = Math.ceil(data.length / studentsPerPage);

    if (data.length === 0) {
      student_list.innerHTML =
        '<tr><td colspan="7" class="text-center text-muted">Không có dữ liệu học sinh</td></tr>';
      return;
    }

    RenderStudentList();
    UpdatePaginationUI();
  } catch (error) {
    console.error("Error fetching students:", error);
    student_list.innerHTML =
      '<tr><td colspan="7" class="text-center text-danger">Lỗi khi tải dữ liệu học sinh. Vui lòng thử lại sau.</td></tr>';
  }
}

function RenderStudentList() {
  const student_list = document.getElementById("student_list");
  if (!student_list || !data.length) return;

  student_list.innerHTML = "";

  let start = (currentPage - 1) * studentsPerPage;
  let end = start + studentsPerPage;

  data.slice(start, end).forEach((student) => {
    const row = `
      <tr>
        <td>${student.id || ""}</td>
        <td>${student.name || ""}</td>
        <td>${student.formatted_dob || student.dob || ""}</td>
        <td>${student.gender?.value || student.gender || ""}</td>
        <td>${student.classroom?.name || "Chưa phân lớp"}</td>
        <td>${student.parent?.name || ""}</td>
        <td>${student.parent?.phone || "0123456789"}</td>
      </tr>
    `;
    student_list.innerHTML += row;
  });
}

function RenderPagination() {
  const pagination = document.getElementById("pagination");
  if (!pagination) return;

  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  if (!prevBtn || !nextBtn) return;

  // Xóa các nút số trang cũ (giữ lại prev và next)
  const pageItems = pagination.querySelectorAll(
    ".page-item:not(#prevBtn):not(#nextBtn)"
  );
  pageItems.forEach((item) => item.remove());

  // Render các nút số trang
  let paginationHTML = "";

  // Tính toán số trang hiển thị
  let startPage = Math.max(1, currentPage - 2);
  let endPage = Math.min(totalPages, currentPage + 2);

  if (startPage > 1) {
    paginationHTML += `<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>`;
    if (startPage > 2) {
      paginationHTML += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
    }
  }

  for (let i = startPage; i <= endPage; i++) {
    const activeClass = i === currentPage ? "active" : "";
    paginationHTML += `<li class="page-item ${activeClass}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
  }

  if (endPage < totalPages) {
    if (endPage < totalPages - 1) {
      paginationHTML += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
    }
    paginationHTML += `<li class="page-item"><a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a></li>`;
  }

  // Chèn vào trước nút next
  nextBtn.insertAdjacentHTML("beforebegin", paginationHTML);

  // Cập nhật trạng thái prev/next
  prevBtn.classList.toggle("disabled", currentPage === 1);
  nextBtn.classList.toggle("disabled", currentPage === totalPages);
}

function UpdatePaginationUI() {
  RenderPagination();
}

function handlePaginationClick(e) {
  const link = e.target.closest(".page-link");
  if (!link || link.classList.contains("disabled")) return;

  e.preventDefault();
  const page = link.dataset.page;

  if (page === "prev" && currentPage > 1) {
    currentPage--;
  } else if (page === "next" && currentPage < totalPages) {
    currentPage++;
  } else if (!isNaN(page)) {
    currentPage = Number(page);
  }

  RenderStudentList();
  UpdatePaginationUI();
}

function AttachPaginationListeners() {
  const pagination = document.getElementById("pagination");
  if (!pagination) return;

  // Chỉ attach một lần bằng cách kiểm tra flag
  if (pagination.dataset.listenerAttached === "true") return;

  // Sử dụng event delegation
  pagination.addEventListener("click", handlePaginationClick);
  pagination.dataset.listenerAttached = "true";
}

function init() {
  AttachPaginationListeners();
  fetchStudents();
}

// Chờ DOM sẵn sàng
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
