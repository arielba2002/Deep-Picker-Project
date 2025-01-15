export const registerUser = async (userData) => {
    const response = await fetch("http://localhost:8888/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });
  
    if (!response.ok) {
      throw new Error("Failed to register user");
    }
  
    return response.json();
  };
  