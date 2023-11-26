import React from "react";
import axios from "axios";
import Cookies from "js-cookie";
import Snackbar from "../snack_bar/toast";

const csrftoken = Cookies.get("csrfToken");
function SignUpForm() {
  const [state, setState] = React.useState({
    name: "",
    email: "",
    password: "",
    confirm_password: ""
  });
  const [notify, setNotify] = React.useState({
    open: false,
    message: "",
    severity: "success",
    handleClose: () => {
      setNotify((prev) => ({ ...prev, open: false }));
    },
  });
  const handleChange = evt => {
    const value = evt.target.value;
    setState({
      ...state,
      [evt.target.name]: value
    });
  };

  const handleOnSubmit = evt => {
    evt.preventDefault();

    const { name, email, password,confirm_password } = state;
    axios.post("http://localhost:8000/signup/",
        {
            "name": name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password
        },
        {
            headers: {
            "X-CSRFToken": csrftoken,
            }
        }
        )
        .then((res) => {
            console.log(res);
            console.log(res.data);
            const message = res.data.message;
            if (res.data.status===200 || res.data.status===201)
            {
              const cookie= res.data.cookie;
              Cookies.set("user", cookie);
            setNotify({
                open: true,
                message: message,
                severity: "success",
                handleClose: () => {
                setNotify((prev) => ({ ...prev, open: false }));
                },
            });}
            else{
                setNotify({
                    open: true,
                    message: message,
                    severity: "error",
                    handleClose: () => {
                    setNotify((prev) => ({ ...prev, open: false }));
                    },
                });
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            setNotify({
                open: true,
                message: "Server is probably down",
                severity: "error",
                handleClose: () => {
                setNotify((prev) => ({ ...prev, open: false }));
                },
            });
        });
    

      setState({
        ...state,
        password: "",
        confirm_password: ""
      });
  };

  return (
    <div>
      <div className="Signinoncss">
    <div className="form-container sign-up-container">
      <form onSubmit={handleOnSubmit}>
        <h1>Create Account</h1>
        <input
          type="text"
          name="name"
          value={state.name}
          onChange={handleChange}
          placeholder="Name"
        />
        <input
          type="email"
          name="email"
          value={state.email}
          onChange={handleChange}
          placeholder="Email"
        />
        <input
          type="password"
          name="password"
          value={state.password}
          onChange={handleChange}
          placeholder="Password"
        />
        <input
          type="password"
          name="confirm_password"
          value={state.confirm_password}
          onChange={handleChange}
          placeholder="Confirm Password"
        />
        <button>Sign Up</button>
      </form>
    </div>
    </div>
    <Snackbar prop={notify} />
    </div>
  );
}

export default SignUpForm;
