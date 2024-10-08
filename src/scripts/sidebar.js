import SectionsSidebarHighlighter from "./lib/sections-sidebar";

const $level2Headings = document
  .getElementById("page-body")
  ?.querySelectorAll("h2[id]");
const $sidebarItems = document
  .getElementById("page-sidebar")
  ?.querySelectorAll(".tna-sidebar__item");
if ($level2Headings && $sidebarItems) {
  new SectionsSidebarHighlighter($level2Headings, $sidebarItems);
}
