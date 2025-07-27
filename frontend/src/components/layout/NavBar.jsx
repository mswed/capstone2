import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, NavDropdown, Container } from 'react-bootstrap';
import { AuthContext } from '../../context/AuthContext';
import ModalWindow from '../ui/ModalWindow';
import LoginForm from '../forms/LoginForm';
import SignupForm from '../forms/SignupForm';
import { MessageContext } from '../../context/MessageContext';

const NavBar = () => {
  const { token, currentUser, signup, login, logout, isAdmin } = useContext(AuthContext);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const { showMessage } = useContext(MessageContext);

  const navigate = useNavigate();

  const handleLogin = async (username, password) => {
    const res = await login(username, password);
    if (res.success) {
      setShowLoginModal(false);
      showMessage('Login Successfull', 'success');
    } else {
      console.log('failed to login');
      showMessage('Login Failed! Incorrect username or password!', 'danger');
    }
  };

  const handleSignup = async (newUserData) => {
    const res = await signup(newUserData);
    if (res.success) {
      setShowSignupModal(false);
      showMessage('Signup Successfull', 'success');
    } else {
      console.log('failed to login');
      showMessage('Signup Failed!', 'danger');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    showMessage('Logout out!', 'success');
  };

  return (
    <Container>
      <Navbar style={{ backgroundColor: '#413C58' }} variant="dark" expand="lg" className="w-100">
        <ModalWindow
          show={showLoginModal}
          onHide={() => setShowLoginModal(false)}
          title={'Login'}
          form={
            <LoginForm
              onSubmit={handleLogin}
              onSwitchToRegister={() => {
                setShowLoginModal(false);
                setShowSignupModal(true);
              }}
            />
          }
        />
        <ModalWindow
          show={showSignupModal}
          onHide={() => setShowSignupModal(false)}
          title={'Signup!'}
          form={
            <SignupForm
              onSubmit={handleSignup}
              onSwitchToLogin={() => {
                setShowSignupModal(false);
                setShowLoginModal(true);
              }}
            />
          }
        />
        <div className="container-fluid">
          <Navbar.Brand as={Link} to="/">
            {' '}
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
              {isAdmin && (
                <Nav.Link as={Link} to={'/sources'}>
                  Sources
                </Nav.Link>
              )}
              <Nav.Link as={Link} to={'/projects'}>
                Projects
              </Nav.Link>
            </Nav>
            <Nav>
              {token ? (
                <NavDropdown
                  title={
                    <>
                      <i className="bi bi-person me-1"></i>
                      {currentUser}
                    </>
                  }
                  id="user-dropdown"
                  align="end"
                >
                  <NavDropdown.Item as={Link} to="/profile">
                    Profile
                  </NavDropdown.Item>
                  <NavDropdown.Item onClick={handleLogout}>Logout</NavDropdown.Item>
                </NavDropdown>
              ) : (
                <>
                  <Nav.Link
                    style={{ cursor: 'pointer' }}
                    onClick={() => {
                      setShowSignupModal(true);
                    }}
                  >
                    Signup
                  </Nav.Link>
                  <Nav.Link
                    style={{ cursor: 'pointer' }}
                    onClick={() => {
                      setShowLoginModal(true);
                    }}
                  >
                    Login
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
