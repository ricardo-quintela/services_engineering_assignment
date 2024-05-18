import { NavLink } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { JwtPayload } from "../interfaces/jwt";
import axios from "axios";

const NavBar = () => {
    const navigate = useNavigate();

    return (
        <Navbar
            expand="lg"
            className="bg-body-tertiary w-100 position-absolute top-0"
        >
            <Container>
                <Navbar.Brand onClick={() => navigate("/")}>
                    Fisioterapista.com
                </Navbar.Brand>
                {localStorage.getItem("jwt") && (
                    <Navbar.Text>
                        Olá,{" "}
                        {
                            (jwtDecode(localStorage.getItem("jwt") || "") as JwtPayload)
                                .username
                        }
                    </Navbar.Text>
                )}

                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse
                    id="basic-navbar-nav"
                    className="d-flex justify-content-end gap-3"
                >
                    {!localStorage.getItem("jwt") && (
                        <NavLink onClick={() => navigate("/login")}>
                            Entrar
                        </NavLink>
                    )}
                    {!localStorage.getItem("jwt") && (
                        <NavLink onClick={() => navigate("/register")}>
                            Registar
                        </NavLink>
                    )}
                    {localStorage.getItem("jwt") && (
                        <NavLink onClick={() => navigate("/scheduling")}>
                            Marcações
                        </NavLink>
                    )}
                    {localStorage.getItem("jwt") &&
                        (jwtDecode(localStorage.getItem("jwt") || "") as JwtPayload).role ===
                            "admin" && (
                            <NavLink onClick={() => navigate("/admin")}>
                                Administração
                            </NavLink>
                        )}
                    {localStorage.getItem("jwt") && (
                        <NavLink
                            onClick={() => {
                                axios.defaults.headers.common['jwt'] = "";
                                localStorage.removeItem("jwt");
                                navigate("/");
                            }}
                        >
                            Logout
                        </NavLink>
                    )}
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default NavBar;
