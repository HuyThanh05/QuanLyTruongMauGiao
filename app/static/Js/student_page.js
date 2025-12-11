const studentsPerPage = 15;
let currentPage = 1;
let data = [];
let totalPages = 1;
let selectedClass = "all";
let searchTerm = "";
let studentPaginator = null;

async function fetchStudents() {
  const student_list = document.getElementById("student_list");
  if (!student_list) return;

  // Hiển thị loading
  student_list.innerHTML =
    '<tr><td colspan="7" class="text-center"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div> Đang tải dữ liệu...</td></tr>';

  try {
    // Lấy query parameter từ URL nếu có
    let apiUrl = `/api/students?`;
    if (searchTerm) apiUrl += `q=${encodeURIComponent(searchTerm)}&`;
    if (selectedClass !== "all") apiUrl += `class_id=${selectedClass}`;

    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error("Failed to fetch students");
    }

    data = await response.json();
    currentPage = 1;
    totalPages = Math.ceil(data.length / studentsPerPage);

    if (data.length === 0) {
      student_list.innerHTML =
        '<tr><td colspan="7" class="text-center text-muted">Không có dữ liệu học sinh</td></tr>';
      if (studentPaginator) studentPaginator.setTotalPages(1);
      return;
    }

    totalPages = Math.max(1, totalPages);
    if (studentPaginator) {
      studentPaginator.setTotalPages(totalPages);
      studentPaginator.goTo(1);
    } else {
      RenderStudentList();
    }
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

function init() {
  // đọc q từ URL nếu có
  const urlParams = new URLSearchParams(window.location.search);
  searchTerm = (urlParams.get("q") || "").trim();

  studentPaginator = createPaginator({
    paginationId: "pagination",
    prevId: "prevBtn",
    nextId: "nextBtn",
    onPageChange: (page) => {
      currentPage = page;
      RenderStudentList();
    },
  });

  // dropdown filter lớp dùng chung
  initDropdownFilter({
    containerSelector: "#classFilter",
    dataAttr: "class",
    defaultValue: "all",
    onChange: (val) => {
      selectedClass = val;
      fetchStudents();
    },
  });

  // tìm kiếm dùng chung
  initSearchInput({
    formSelector: "#studentSearchForm",
    inputSelector: "#studentSearchInput",
    onSearch: (val) => {
      searchTerm = val;
      fetchStudents();
    },
  }).setValue(searchTerm);

  fetchStudents();
}

// Chờ DOM sẵn sàng
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
