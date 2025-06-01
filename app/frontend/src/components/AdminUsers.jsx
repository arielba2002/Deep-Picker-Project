import React, { useEffect, useState } from "react";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://backend.deep.svc.cluster.local:8888/api/v1/users?limit=100")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch users");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading users...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div style={{padding: '2rem'}}>
      <h2>All Users</h2>
      <table style={{width: '100%', borderCollapse: 'collapse'}}>
        <thead>
          <tr>
            <th style={{border: '1px solid #ccc', padding: '8px'}}>ID</th>
            <th style={{border: '1px solid #ccc', padding: '8px'}}>Name</th>
            <th style={{border: '1px solid #ccc', padding: '8px'}}>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td style={{border: '1px solid #ccc', padding: '8px'}}>{u.id}</td>
              <td style={{border: '1px solid #ccc', padding: '8px'}}>{u.name}</td>
              <td style={{border: '1px solid #ccc', padding: '8px'}}>{u.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
