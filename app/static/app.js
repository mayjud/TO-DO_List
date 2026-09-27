const modal = document.getElementById('taskModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');

if (openModalBtn) {
  openModalBtn.addEventListener('click', () => {
    modal.classList.remove('hidden');
  });
}

if (closeModalBtn) {
  closeModalBtn.addEventListener('click', () => modal.classList.add('hidden'));
}

if (cancelModalBtn) {
  cancelModalBtn.addEventListener('click', () => modal.classList.add('hidden'));
}

window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.classList.add('hidden');
  }
});
