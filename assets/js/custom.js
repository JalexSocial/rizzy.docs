// Put your custom JS code here

// Wide Markdown tables scroll inside their own container instead of widening the page on phones.
// A wrapper keeps the <table> element (and its semantics) unchanged; `display: block` on the table
// itself would drop table semantics in some screen readers.
document.querySelectorAll('.docs-content table').forEach((table) => {
  if (table.closest('.table-responsive, .highlight')) {
    return;
  }

  const wrapper = document.createElement('div');
  wrapper.className = 'table-responsive docs-table';
  table.parentNode.insertBefore(wrapper, table);
  wrapper.appendChild(table);
});
