// import { invoke } from '@tauri-apps/api/tauri';

// let greetInputEl: HTMLInputElement | null;
// let greetMsgEl: HTMLElement | null;

// async function greet() {
//   if (greetMsgEl && greetInputEl) {
//     // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
//     greetMsgEl.textContent = await invoke('greet', {
//       name: greetInputEl.value,
//     });
//   }
// }
// let status: String | `Link ⬆️ aca` ;
const input = document.getElementById('link') as HTMLInputElement;

function limpiarInput() {
  input.value = '';
}
input.addEventListener('click',limpiarInput)

window.addEventListener('DOMContentLoaded', () => {
  let currentStatus = document.getElementById('status');
  if (currentStatus === null) {
    console.log('Input error')  
  }
  else if (currentStatus.innerText === `Loading`) {
    currentStatus.innerText = `Link ⬆️ aca`;
    console.log(typeof currentStatus)  
  }
})





// window.addEventListener('DOMContentLoaded', () => {

//   greetInputEl = document.querySelector('#greet-input');
//   greetMsgEl = document.querySelector('#greet-msg');
//   document.querySelector('#greet-form')?.addEventListener('submit', (e) => {
//     e.preventDefault();
//     greet();
//   });
// });
