import { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { AuthContext } from '../../context/AuthContext';
// import { MessageContext } from './MessageContext';

const NavBar = () => {
  const { token, currentUser, logout } = useContext(AuthContext);
  // const { showMessage } = useContext(MessageContext);

  const navigate = useNavigate();
  return (
    <Container>
      <Navbar style={{ backgroundColor: '#413C58' }} variant="dark" expand="lg" className="w-100">
        <div className="container-fluid">
          <Navbar.Brand as={Link} to="/">
            <img src="/grumpy-logo.png" height="75" className="d-inline-block align-top" alt="Grumpy Tracker Logo" />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link as={Link} to={'/makes'}>
                Makes
              </Nav.Link>
              <Nav.Link as={Link} to={'/cameras'}>
                Cameras
              </Nav.Link>
              <Nav.Link as={Link} to={'/formats'}>
                Formats
              </Nav.Link>
              <Nav.Link as={Link} to={'/sources'}>
                Sources
              </Nav.Link>
              <Nav.Link as={Link} to={'/projects'}>
                Projects
              </Nav.Link>
              {token ? (
                <>
                  <Nav.Link as={Link} to={'/profile'}>
                    Profile
                  </Nav.Link>
                  <Nav.Link
                    style={{ cursor: 'pointer' }}
                    onClick={() => {
                      navigate('/');
                      logout();
                      // showMessage('You have successfully logged out!', 'success');
                    }}
                  >
                    Logout ({currentUser})
                  </Nav.Link>
                </>
              ) : (
                <>
                  <Nav.Link as={Link} to={'/login'}>
                    Login
                  </Nav.Link>
                  <Nav.Link as={Link} to={'/signup'}>
                    Signup
                  </Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </div>
      </Navbar>
    </Container>
  );
};

export default NavBar;
