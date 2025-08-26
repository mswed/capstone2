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

        <h5>Can I add a Make, Camera or Format myself?</h5>
        <Card.Body>
          Not yet! At the moment, to make sure the data is as accurate as possible registered users can only add projects, assign formats to a project from the list of existing
          formats, and vote on the usefulness of the attached format. In the future I plan to have at least a few moderators who can add makes, cameras and formats.
        </Card.Body>

        <h5>Ok, but... I don't see the Make/Camera/Format I need...</h5>
        <Card.Body>
          Just send me an email to grumpy@beapot.com with the the details you need added and (if you have it) the source of the data. The more information you give me the better!
        </Card.Body>

        <h5>What are projects good for?</h5>
        <Card.Body>
          The idea is to create a shared database between studios that can tell matchmove artists which cameras and formats were used on the project. The idea is that users will
          add the project they are working on, and attach the camera/format information to it. Other users can then search for the project and up vote or down vote the format based
          on whether or not it worked for them.
        </Card.Body>

        <h5>How do I add a project?</h5>
        <Card.Body>
          First make sure you are registered and logged in. Anonymous users can not add or edit projects. Go to the projects tab and search for your project. If you're lucky, the
          project is already in the database and will appear in the In Database section of the page. If not, you should see results from TMDB with all the movies/tv shows that
          match your search. Once you find the project on TMDB you can click the 'Add' button and the project will be added to the grumpy tracker! If you can't find the project in
          our database or TMDB I'm afraid that for the moment you are out of luck. Future version of the site will allow you to add projects that are not yet on TMDB, but that will
          take a while.
        </Card.Body>

        <h5>How do I add a format/camera to a project?</h5>
        <Card.Body>
          First make sure you are registered and logged in. Anonymous users can not add or edit projects. Find the project in the projects tab and click 'View'. Once you see the
          project details you should have an 'Add Format' button. Once you click it a window will open with all the formats we currently have in the database, search for the format
          you need and click the 'Add' button. Cameras can not be added on their own, but if you add a format its camera will also be attached to the project. take a while.
        </Card.Body>
      </Card>
    </Container>
  );
};

export default About;
