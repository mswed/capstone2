import { useState } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';

const SimpleSearchFrom = ({ fields, targetArray, setTargetArray, originalArray }) => {
  const INITIAL_STATE = '';
  const [searchTerm, setSearchTerm] = useState(INITIAL_STATE);
  const handleChange = (evt) => {
    setSearchTerm(evt.target.value);
  };

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (!searchTerm) {
      setTargetArray(originalArray);
    } else {
      // For each of our fields check if the search term was found and filter our main array based
      // on that
      const results = targetArray.filter((item) => fields.some((field) => item[field].toLowerCase().includes(searchTerm.toLowerCase())));
      setTargetArray([...results]);
    }
  };
  return (
    <Form onSubmit={handleSubmit}>
      <InputGroup className="my-3">
        <Form.Control placeholder="Enter search term..." onChange={handleChange} value={searchTerm} />
        <Button variant="primary" type="submit">
          Search!
        </Button>
      </InputGroup>
    </Form>
  );
};

export default SimpleSearchFrom;
