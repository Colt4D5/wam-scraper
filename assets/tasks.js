const tasks = document.querySelectorAll('.summary-content')
const checkboxes = document.querySelectorAll('.checkbox')
const contents = document.querySelectorAll('.content')

checkboxes.forEach(check => {
	check.addEventListener('click', e => {
		const checkbox = e.target.closest('.checkbox')

		checkbox.classList.toggle('active')
	})
})

tasks.forEach(task => {
	task.addEventListener('click', e => {
		if (e.target.closest('.checkbox')) return;

		const content = e.target.closest('.summary').lastElementChild

		// tasks.forEach(t => {
		// 	if (t != content) {
		// 		t.nextElementSibling.classList.remove('active')
		// 	}
		// })

		content.classList.toggle('active')

		if (content.classList.contains('active')) {
			content.style.maxHeight = content.scrollHeight + 'px'
		} else content.style.maxHeight = 0 + 'px'
	})
})

contents.forEach(content => {
	content.addEventListener('click', e => {
		navigator.clipboard.writeText(e.target.innerText)
		// copyToClipboard(e.target.innerText)
	})
})

function copyToClipboard(text) {
    if (window.clipboardData) { // Internet Explorer
        window.clipboardData.setData("Text", text);
    } else {
        unsafeWindow.netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
        const clipboardHelper = Components.classes["@mozilla.org/widget/clipboardhelper;1"].getService(Components.interfaces.nsIClipboardHelper);
        clipboardHelper.copyString(text);
    }
}