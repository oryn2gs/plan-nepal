export const validatePassword = (password) => {
  const patterns =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
  const passwordValid = password.length > 8 && patterns.test(password);

  if (!passwordValid) return false;
  return true;
};
