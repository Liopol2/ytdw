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
const formato:string="";
function limpiarInput() {
  input.value = '';
}
// function descargar(formato:string,calidad:string,playlist:boolean){
//   if (playlist===true){
//     songs.forEach(song => {
//       //download
//     });
//   }

  switch (formato){
    case 'Video':
      //  descargar video
    case 'Audio':
      //  descargar audio
    case 'Transcripción':
      //  descargar transcripción
    break;
  }
  
input.addEventListener('click',limpiarInput)
//input.addEventListener('paste',descargar)
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



