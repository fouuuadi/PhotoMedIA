  const email = "{{ email_user|escapejs }}";  
  if (email) {
    localStorage.setItem("email_user", email);
  }