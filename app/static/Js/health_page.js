const healthPerPage = 10;
let healthCurrentPage = 1;
let healthTotalPages = 1;
let healthRows = [];
let healthFilteredRows = [];
let healthPaginator = null;
let healthSelectedClass = "all";
let healthSearch = "";

function renderHealthPage() {
  const start = (healthCurrentPage - 1) * healthPerPage;
  const end = start + healthPerPage;

  // Ẩn tất cả trước
  healthRows.forEach((row) => (row.style.display = "none"));

  healthFilteredRows.forEach((row, idx) => {
    row.style.display = idx >= start && idx < end ? "" : "none";
  });
}

function initHealthPagination() {
  const tbody = document.getElementById("health_list");
  if (!tbody) return;

  healthRows = Array.from(tbody.querySelectorAll("tr"));
  healthFilteredRows = [...healthRows];
  healthTotalPages = Math.max(1, Math.ceil(healthRows.length / healthPerPage));

  healthPaginator = createPaginator({
    paginationId: "pagination-health",
    prevId: "prevBtnHealth",
    nextId: "nextBtnHealth",
    onPageChange: (page) => {
      healthCurrentPage = page;
      renderHealthPage();
    },
  });

  if (healthPaginator) {
    healthPaginator.setTotalPages(healthTotalPages);
    healthPaginator.goTo(1);
  }

  // Filter lớp
  initDropdownFilter({
    containerSelector: "#classFilterHealth",
    dataAttr: "class",
    defaultValue: "all",
    onChange: (val) => {
      healthSelectedClass = val;
      applyHealthFilters();
    },
  });

  // Tìm kiếm
  initSearchInput({
    formSelector: "#healthSearchForm",
    inputSelector: "#healthSearchInput",
    onSearch: (val) => {
      healthSearch = val.toLowerCase();
      applyHealthFilters();
    },
  });
}

function applyHealthFilters() {
  healthFilteredRows = healthRows.filter((row) => {
    const classId = row.dataset.classId;
    const name = (row.dataset.studentName || "").toLowerCase();
    const matchClass =
      healthSelectedClass === "all" ||
      (classId && String(classId) === String(healthSelectedClass));
    const matchSearch = !healthSearch || name.includes(healthSearch);
    return matchClass && matchSearch;
  });

  healthTotalPages = Math.max(
    1,
    Math.ceil(healthFilteredRows.length / healthPerPage)
  );
  if (healthPaginator) {
    healthPaginator.setTotalPages(healthTotalPages);
    healthPaginator.goTo(1);
  } else {
    renderHealthPage();
  }
}

// Chờ DOM sẵn sàng
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initHealthPagination);
} else {
  initHealthPagination();
}
