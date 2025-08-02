import { Container, Card } from 'react-bootstrap';

const About = () => {
  return (
    <Container className="text-start">
      <Card className="shadow-lg rounded-0 rounded-bottom text-start p-3">
        <Card.Title>About The Grumpy Tracker</Card.Title>
        <Card.Text>
          The Grumpy Tracker is a website geared toward the Tracking/Matchmove VFX artists community. It has a collection of camera formats with (hopefully) all the information
          needed to start setting up a solve in your favorite tracking software. While the website is geared slightly more toward 3DEqualizer users, the data it contains can be
          used anywhere.
        </Card.Text>
      </Card>
      <Card className="shadow-lg mt-3 p-3">
        <Card.Title>FAQ</Card.Title>
        <h5>What kind of information do you have?</h5>
        <Card.Body>
          The website contains filmback and recording resolution data for various cameras and makes. It also has some 3de specific information such as the best distortion model to
          use and (in some cases) a 3de specific filmback that does not fully match the manufacturers info. In such cases a note will be clearly displayed on the format. There is
          also a Projects section, where users can add projects they are working on (assuming they can be found on TMDB) and assign a format/camera to them. Other users can then
          see the project's formats and vote on them.
        </Card.Body>
      </Card>
    </Container>
  );
};

export default About;
