import { useState, useEffect, useContext } from 'react';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import { AuthContext } from '../../context/AuthContext';
import Loading from '../../components/ui/Loading';
import ProfileDetailsForm from '../../components/forms/ProfileDetailsForm';
import PasswordUpdateForm from '../../components/forms/PasswordUpdateForm';

const Profile = () => {
  const { userId, isInitialized } = useContext(AuthContext);
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const handleUpdateUser = async (updatedUserData) => {
    try {
      const updatedUserDetails = await GrumpyApi.updateUser(userId, updatedUserData);
      setUserData((prev) => ({ ...prev, ...updatedUserDetails }));
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  };

  // Fetch user data
  useEffect(() => {
    const getUserDetails = async () => {
      // If we don't have a user yet don't bother searching
      if (!userId || !isInitialized) {
        return;
      }

      setIsLoading(true);
      try {
        const response = await GrumpyApi.getUserDetails(userId);
        setUserData(response);
      } catch (error) {
        console.error('Error fetching user details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getUserDetails();
  }, [userId, isInitialized]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <Card className="shadow-lg rounded-0 rounded-bottom pt-3 px-1">
        <Row>
          <Col className="text-start">
            <Card className="shadow-lg rounded p-3 m-1">
              <Card.Title>Profile Details</Card.Title>
              <ProfileDetailsForm userData={userData} onSubmit={handleUpdateUser} />
            </Card>
          </Col>
          <Col className="text-start">
            <Card className="shadow-lg rounded p-3 m-1">
              <Card.Title>Login Details</Card.Title>
              <PasswordUpdateForm username={userData.username} onSubmit={handleUpdateUser} />
            </Card>
          </Col>
        </Row>
      </Card>
    </Container>
  );
};

export default Profile;
