// Ripple effect for nav buttons. Used copilot to help generate this code.
// Source: https://css-tricks.com/how-to-recreate-the-ripple-effect-of-material-design-buttons/
document.addEventListener('DOMContentLoaded', function() {
	const buttons = document.querySelectorAll('#buttons a');
	buttons.forEach(btn => {
		btn.addEventListener('mouseenter', e => {
            console.log(`Hovering over ${btn.href}`);
			const ripple = document.createElement('span');
			ripple.className = 'ripple';
			const rect = btn.getBoundingClientRect();
			const size = Math.max(rect.width, rect.height);
			ripple.style.width = ripple.style.height = size + 'px';
			ripple.style.left = (e.clientX - rect.left - size/2) + 'px';
			ripple.style.top = (e.clientY - rect.top - size/2) + 'px';
			btn.appendChild(ripple);
			ripple.addEventListener('animationend', () => ripple.remove());
		});
        btn.addEventListener('click', () => {
            console.log(`Navigating to ${btn.href}`);
		});
	});
});
