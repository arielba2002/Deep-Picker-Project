import React from "react";
import RegisterForm from "../components/RegisterForm";

const RegisterPage = () => {
  const handleSuccess = (user) => {
    alert(`User ${user.name} registered successfully!`);
  };

  return (
    <div>
      <h1>Register</h1>
      <RegisterForm onSuccess={handleSuccess} />
    </div>
  );
};

export default RegisterPage;
