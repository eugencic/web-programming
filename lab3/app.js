"use strict";

window.addEventListener('load', () => {
	const form = document.querySelector("#new-task-form");
	const input = document.querySelector("#new-task-input");
	const tasks = document.querySelector("#tasks");
	const filter_container = document.querySelector("#filter-container");
	const filter = document.querySelector("#filter");

	if (tasks.children.length === 0) {
		filter_container.style.display = "none";
	} else {
		filter_container.style = document.querySelectorAll("filter-container");
	}

	form.addEventListener('submit', (e) => {
		e.preventDefault();

		const task = input.value;

		if (task === "") {
			return
		}

		const task_el = document.createElement('div');
		task_el.classList.add('task');

		const task_content_el = document.createElement('div');
		task_content_el.classList.add('content');

		task_el.appendChild(task_content_el);

		const task_input_el = document.createElement('input');
		task_input_el.classList.add('text');
		task_input_el.type = 'text';
		task_input_el.value = task;
		task_input_el.setAttribute('readonly', 'readonly');

		task_content_el.appendChild(task_input_el);

		const task_actions_el = document.createElement('div');
		task_actions_el.classList.add('actions');

		const task_check_el = document.createElement('button');
		task_check_el.classList.add('to-do');
		task_check_el.innerText = 'To-do';
		
		const task_edit_el = document.createElement('button');
		task_edit_el.classList.add('edit');
		task_edit_el.innerText = 'Edit';

		const task_delete_el = document.createElement('button');
		task_delete_el.classList.add('delete');
		task_delete_el.innerText = 'Delete';

		task_actions_el.appendChild(task_check_el)
		task_actions_el.appendChild(task_edit_el);
		task_actions_el.appendChild(task_delete_el);

		task_el.appendChild(task_actions_el);

		tasks.appendChild(task_el);

		input.value = '';

		task_check_el.addEventListener('click', (e) => {
			if (task_check_el.innerText.toLowerCase() == "to-do") {
				task_check_el.innerText = "Done";
				task_el.style.backgroundColor = "var(--greyDark)";

				var filter = document.getElementById("filter");
				var strfilter = filter.value;
				
				if (strfilter == "all") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "to-do") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--darkest)";
						} else {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--greyDark)";
						}
					});
				} else if (strfilter == "to-do") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "to-do") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--darkest)";
						} else {
							taskEl.style.display = "none";
						}
					});
				} else if (strfilter == "done") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "done") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--greyDark)";
						} else {
							taskEl.style.display = "none";
						}
					});
				}
			} else if (task_check_el.innerText.toLowerCase() == "done") {
				task_check_el.innerText = "To-do";
				task_el.style.backgroundColor = "var(--darkest)";
				var filter = document.getElementById("filter");
				var strfilter = filter.value;
				
				if (strfilter == "all") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "to-do") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--darkest)";
						} else {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--greyDark)";
						}
					});
				} else if (strfilter == "to-do") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "to-do") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--darkest)";
						} else {
							taskEl.style.display = "none";
						}
					});
				} else if (strfilter == "done") {
					const taskEls = document.querySelectorAll(".task");
					taskEls.forEach(taskEl => {
						const checkBtn = taskEl.querySelector(".to-do");
						if (checkBtn.innerText.toLowerCase() === "done") {
							taskEl.style = document.querySelectorAll(".task");
							taskEl.style.backgroundColor = "var(--greyDark)";
						} else {
							taskEl.style.display = "none";
						}
					});
				}
			}
		});

		if (tasks.children.length === 0) {
			filter_container.style.display = "none";
		} else {
			filter_container.style = document.querySelectorAll("filter-container");
		}

		task_edit_el.addEventListener('click', (e) => {
			if (task_edit_el.innerText.toLowerCase() == "edit") {
				task_edit_el.innerText = "Save";
				task_input_el.removeAttribute("readonly");
				task_input_el.focus();
			} else {
				task_edit_el.innerText = "Edit";
				task_input_el.setAttribute("readonly", "readonly");
			}
		});

		task_delete_el.addEventListener('click', (e) => {
			tasks.removeChild(task_el);
			if (tasks.children.length === 0) {
				filter_container.style.display = "none";
			} else {
				filter_container.style = document.querySelectorAll("filter-container");
			}
		});
	});

	filter.addEventListener("click", () => {
		var filter = document.getElementById("filter");
		var strfilter = filter.value;
		if (strfilter == "all") {
			const taskEls = document.querySelectorAll(".task");
			taskEls.forEach(taskEl => {
				const checkBtn = taskEl.querySelector(".to-do");
				if (checkBtn.innerText.toLowerCase() === "to-do") {
					taskEl.style = document.querySelectorAll(".task");
					taskEl.style.backgroundColor = "var(--darkest)";
				} else {
					taskEl.style = document.querySelectorAll(".task");
					taskEl.style.backgroundColor = "var(--greyDark)";
				}
			});
		} else if (strfilter == "to-do") {
			const taskEls = document.querySelectorAll(".task");
			taskEls.forEach(taskEl => {
				const checkBtn = taskEl.querySelector(".to-do");
				if (checkBtn.innerText.toLowerCase() === "to-do") {
					taskEl.style = document.querySelectorAll(".task");
					taskEl.style.backgroundColor = "var(--darkest)";
				} else {
					taskEl.style.display = "none";
				}
			});
		} else if (strfilter == "done") {
			const taskEls = document.querySelectorAll(".task");
			taskEls.forEach(taskEl => {
				const checkBtn = taskEl.querySelector(".to-do");
				if (checkBtn.innerText.toLowerCase() === "done") {
					taskEl.style = document.querySelectorAll(".task");
					taskEl.style.backgroundColor = "var(--greyDark)";
				} else {
					taskEl.style.display = "none";
				}
			});
		}
	});
})