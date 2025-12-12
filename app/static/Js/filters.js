/**
 * Khởi tạo dropdown filter dùng chung.
 * @param {Object} options
 * @param {string} options.containerSelector - selector của container chứa dropdown-items
 * @param {string} [options.itemSelector=".dropdown-item"] - selector cho item
 * @param {string} [options.dataAttr="class"] - tên data-* chứa giá trị filter
 * @param {string} [options.defaultValue="all"] - giá trị mặc định
 * @param {(value:string)=>void} options.onChange - callback khi đổi giá trị
 */
function initDropdownFilter({
  containerSelector,
  itemSelector = ".dropdown-item",
  dataAttr = "class",
  defaultValue = "all",
  onChange,
  toggleSelector,
  activeClass = "active",
}) {
  const container = document.querySelector(containerSelector);
  const toggleBtn = toggleSelector
    ? document.querySelector(toggleSelector)
    : null;

  if (!container) return { setValue: () => {}, getValue: () => defaultValue };

  let current = defaultValue;

  container.querySelectorAll(itemSelector).forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const value = this.dataset[dataAttr];
      current = value ?? defaultValue;

      // cập nhật nhãn nút toggle nếu có
      if (toggleBtn) {
        toggleBtn.textContent = this.textContent.trim();
      }

      // cập nhật trạng thái active
      if (activeClass) {
        container.querySelectorAll(itemSelector).forEach((el) => {
          el.classList.toggle(activeClass, el === this);
        });
      }

      onChange?.(current);
    });
  });

  const api = {
    setValue(val) {
      current = val ?? defaultValue;
      onChange?.(current);

      // đồng bộ nhãn toggle theo item khớp
      if (toggleBtn) {
        const matched = Array.from(
          container.querySelectorAll(itemSelector)
        ).find((el) => el.dataset[dataAttr] === current);
        if (matched) {
          toggleBtn.textContent = matched.textContent.trim();
        }
      }
    },
    getValue() {
      return current;
    },
  };

  // khởi tạo nhãn toggle mặc định
  api.setValue(defaultValue);

  return api;
}

/**
 * Khởi tạo tìm kiếm bằng form/input.
 * @param {Object} options
 * @param {string} options.formSelector - selector form
 * @param {string} options.inputSelector - selector input
 * @param {(value:string)=>void} options.onSearch - callback khi submit/enter
 */
function initSearchInput({ formSelector, inputSelector, onSearch }) {
  const form = document.querySelector(formSelector);
  const input = document.querySelector(inputSelector);
  if (!form || !input) return { setValue: () => {} };

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    onSearch?.(input.value.trim());
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      onSearch?.(input.value.trim());
    }
  });

  return {
    setValue(val) {
      input.value = val ?? "";
    },
    getValue() {
      return input.value.trim();
    },
  };
}
