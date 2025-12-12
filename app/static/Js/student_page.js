const studentsPerPage = 15;
let currentPage = 1;
let data = [];
let totalPages = 1;
let selectedClass = "all";
let searchTerm = "";
let studentPaginator = null;
let editModal = null;
let parentOptions = [];

// Tải danh sách học sinh từ API theo bộ lọc tìm kiếm/lớp và cập nhật bảng + phân trang
async function fetchStudents() {
  const student_list = document.getElementById("student_list");
  if (!student_list) return;

  // Hiển thị loading
  student_list.innerHTML =
    '<tr><td colspan="8" class="text-center"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div> Đang tải dữ liệu...</td></tr>';

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
    buildParentOptions();
    currentPage = 1;
    totalPages = Math.ceil(data.length / studentsPerPage);

    if (data.length === 0) {
      student_list.innerHTML =
        '<tr><td colspan="8" class="text-center text-muted">Không có dữ liệu học sinh</td></tr>';
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
      '<tr><td colspan="8" class="text-center text-danger">Lỗi khi tải dữ liệu học sinh. Vui lòng thử lại sau.</td></tr>';
  }
}

// Render bảng học sinh cho trang hiện tại dựa trên dữ liệu đã tải
function RenderStudentList() {
  const student_list = document.getElementById("student_list");
  if (!student_list || !data.length) return;

  student_list.innerHTML = "";

  let start = (currentPage - 1) * studentsPerPage;
  let end = start + studentsPerPage;

  data.slice(start, end).forEach((student) => {
    const row = `
      <tr>
        <td>${student.id}</td>
        <td>${student.name}</td>
        <td>${student.dob || student.formatted_dob}</td>
        <td>${student.gender?.value || student.gender}</td>
        <td>${student.classroom?.name || "Chưa phân lớp"}</td>
        <td>${student.parent?.name}</td>
        <td>${student.parent?.phone}</td>
        <td class="text-end">
          <button
            class="btn btn-sm btn-outline-primary"
            data-id="${student.id}"
            aria-label="Chỉnh sửa học sinh ${student.name}"
          >
            Chỉnh sửa
          </button>
        </td>
      </tr>
    `;
    student_list.innerHTML += row;
  });
}

// Gom danh sách phụ huynh từ dữ liệu hiện có (unique theo id) để fill datalist
function buildParentOptions() {
  const seen = new Set();
  parentOptions = [];
  data.forEach((s) => {
    if (s.parent?.id && !seen.has(s.parent.id)) {
      seen.add(s.parent.id);
      parentOptions.push({
        id: s.parent.id,
        name: s.parent.name || "",
        phone: s.parent.phone || "",
      });
    }
  });

  const datalist = document.getElementById("parentOptions");
  if (!datalist) return;
  datalist.innerHTML = "";

  parentOptions.forEach((p) => {
    const label = `${p.name || "Không tên"} - ${p.phone || "Không số"}`;
    const opt = document.createElement("option");
    opt.value = label;
    opt.dataset.id = p.id;
    datalist.appendChild(opt);
  });
}

// Mở modal và đổ dữ liệu học sinh
function openEditModal(student) {
  if (!student) return;
  document.getElementById("editStudentId").value = student.id || "";
  document.getElementById("editStudentName").value = student.name || "";
  document.getElementById("editStudentDob").value =
    student.dob || student.formatted_dob || "";
  document.getElementById("editStudentGender").value =
    student.gender?.value || student.gender || "";
  document.getElementById("editStudentClassSelect").value =
    student.class_id || student.classroom?.id || "";

  const parentId = student.parent?.id || "";
  const parentLabel = parentOptions.find(
    (p) => String(p.id) === String(parentId)
  );
  document.getElementById("editParentFilter").value = parentLabel
    ? `${parentLabel.name || "Không tên"} - ${parentLabel.phone || "Không số"}`
    : "";
  document.getElementById("editStudentParentId").value = parentId || "";
  document.getElementById("editStudentError").textContent = "";

  if (!editModal) {
    const modalEl = document.getElementById("editStudentModal");
    if (!modalEl) return;
    editModal = new bootstrap.Modal(modalEl);
  }
  editModal.show();
}

// Lưu chỉnh sửa qua API PATCH
async function saveStudent() {
  const studentId = document.getElementById("editStudentId")?.value;
  if (!studentId) return;

  const name = document.getElementById("editStudentName")?.value.trim();
  const dob = document.getElementById("editStudentDob")?.value.trim();
  const gender = document.getElementById("editStudentGender")?.value;
  const classId = document.getElementById("editStudentClassSelect")?.value;
  const parentId = document.getElementById("editStudentParentId")?.value;
  const errorEl = document.getElementById("editStudentError");
  if (errorEl) errorEl.textContent = "";

  let payload = {
    name,
    dob,
    gender,
    class_id: classId ? Number(classId) : null,
    parent_id: parentId ? Number(parentId) : null,
  };

  // Xóa các field không có giá trị
  Object.keys(payload).forEach(
    (key) => payload[key] == null && delete payload[key]
  );

  try {
    const res = await fetch(`/api/students/${studentId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      if (errorEl) errorEl.textContent = data.message || "Cập nhật thất bại";
      else alert("Lỗi cập nhật: " + (data.message || "Cập nhật thất bại"));
      return;
    }

    if (editModal) editModal.hide();
    fetchStudents();
  } catch (err) {
    console.error(err);
    if (errorEl) errorEl.textContent = err.message || "Có lỗi xảy ra";
    else alert("Có lỗi xảy ra");
  }
}

// Khởi tạo bộ lọc, tìm kiếm, phân trang và gọi fetch lần đầu
function init() {
  // đọc q từ URL nếu có
  const urlParams = new URLSearchParams(window.location.search);
  searchTerm = (urlParams.get("q") || "").trim();

  if (typeof createPaginator === "function") {
    studentPaginator = createPaginator({
      paginationId: "pagination",
      prevId: "prevBtn",
      nextId: "nextBtn",
      onPageChange: (page) => {
        currentPage = page;
        RenderStudentList();
      },
    });
  }

  // dropdown filter lớp dùng chung
  if (typeof initDropdownFilter === "function") {
    const df = initDropdownFilter({
      containerSelector: "#classFilter",
      dataAttr: "class",
      defaultValue: "all",
      toggleSelector: "#classFilterToggle",
      onChange: (val) => {
        selectedClass = val;
        fetchStudents();
      },
    });
    // đồng bộ nút toggle với giá trị mặc định
    df.setValue(selectedClass);
  }

  // tìm kiếm dùng chung
  if (typeof initSearchInput === "function") {
    initSearchInput({
      formSelector: "#studentSearchForm",
      inputSelector: "#studentSearchInput",
      onSearch: (val) => {
        searchTerm = val;
        fetchStudents();
      },
    }).setValue(searchTerm);
  }

  fetchStudents();

  // Ủy quyền sự kiện click nút chỉnh sửa
  const student_list = document.getElementById("student_list");
  if (student_list) {
    student_list.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-id]");
      if (!btn) return;
      const id = btn.getAttribute("data-id");
      const student = data.find((s) => String(s.id) === String(id));
      openEditModal(student);
    });
  }

  // Sự kiện lưu trong modal
  const saveBtn = document.getElementById("saveStudentBtn");
  if (saveBtn) {
    saveBtn.addEventListener("click", saveStudent);
  }

  // Lọc & chọn phụ huynh bằng 1 ô nhập + datalist
  const parentFilter = document.getElementById("editParentFilter");
  const parentIdHidden = document.getElementById("editStudentParentId");
  const parentDatalist = document.getElementById("parentOptions");
  if (parentFilter && parentIdHidden && parentDatalist) {
    parentFilter.addEventListener("input", () => {
      const val = parentFilter.value;
      const opt = Array.from(parentDatalist.options).find(
        (o) => o.value === val && o.dataset.id
      );
      parentIdHidden.value = opt ? opt.dataset.id : "";
    });
  }
}

// Chờ DOM sẵn sàng
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
