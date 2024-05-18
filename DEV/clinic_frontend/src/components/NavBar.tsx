import { NavLink } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { useNavigate } from "react-router-dom";
import { getCookies, setCookie } from "../cookies";
import { jwtDecode } from "jwt-decode";
import { JwtPayload } from "../interfaces/jwt";

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
                {getCookies()["jwt"] && (
                    <Navbar.Text>
                        Olá,{" "}
                        {
                            (jwtDecode(getCookies()["jwt"]) as JwtPayload)
                                .username
                        }
                    </Navbar.Text>
                )}

                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse
                    id="basic-navbar-nav"
                    className="d-flex justify-content-end gap-3"
                >
                    {!getCookies()["jwt"] && (
                        <NavLink onClick={() => navigate("/login")}>
                            Entrar
                        </NavLink>
                    )}
                    {!getCookies()["jwt"] && (
                        <NavLink onClick={() => navigate("/register")}>
                            Registar
                        </NavLink>
                    )}
                    {getCookies()["jwt"] && (
                        <NavLink onClick={() => navigate("/scheduling")}>
                            Marcações
                        </NavLink>
                    )}
                    {getCookies()["jwt"] &&
                        (jwtDecode(getCookies()["jwt"]) as JwtPayload).role ===
                            "admin" && (
                            <NavLink onClick={() => navigate("/admin")}>
                                Administração
                            </NavLink>
                        )}
                    {getCookies()["jwt"] && (
                        <NavLink
                            onClick={() => {
                                setCookie("jwt", "");
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
