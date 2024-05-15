import { NavLink } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { useNavigate } from "react-router-dom";


const NavBar = () => {

    const navigate = useNavigate();

    return (
        <Navbar
            expand="lg"
            className="bg-body-tertiary w-100 position-absolute top-0"
        >
            <Container>
                <Navbar.Brand onClick={() => navigate("/")}>Fisioterapista.com</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                        <NavLink onClick={() => navigate("/login")}>Entrar</NavLink>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default NavBar;
