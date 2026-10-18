const menu=document.querySelector('.menu-toggle');
const navigation=document.querySelector('.nav');
menu?.addEventListener('click',()=>{
  const open=menu.getAttribute('aria-expanded')!=='true';
  menu.setAttribute('aria-expanded',String(open));
  menu.textContent=open?'Close':'Menu';
  navigation.classList.toggle('open',open);
});
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){
    menu.click();menu.focus();
  }
});
