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
}) {
  const container = document.querySelector(containerSelector);
  if (!container) return { setValue: () => {} };

  let current = defaultValue;

  container.querySelectorAll(itemSelector).forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const value = this.dataset[dataAttr];
      current = value ?? defaultValue;
      onChange?.(current);
    });
  });

  return {
    setValue(val) {
      current = val ?? defaultValue;
      onChange?.(current);
    },
    getValue() {
      return current;
    },
  };
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
