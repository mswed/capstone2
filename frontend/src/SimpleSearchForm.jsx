import { useState } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';

const SimpleSearchFrom = ({ fields, targetArray, setTargetArray, originalArray }) => {
  const INITIAL_STATE = '';
  const [searchTerm, setSearchTerm] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    // Grab the new value
    const value = evt.target.value;
    // Set the state
    setSearchTerm(value);

    // Filter
    if (value.trim() === '') {
      // We did not search for anything show original data
      setTargetArray(originalArray);
    } else {
      // Filter the list
      const results = targetArray.filter((item) => fields.some((field) => item[field]?.toLowerCase().includes(searchTerm.toLowerCase())));
      setTargetArray([...results]);
    }
  };

  const handleClear = () => {
    setSearchTerm('');
    setTargetArray(originalArray);
  };

  return (
    <Form>
      <InputGroup className="my-3">
        <Form.Control placeholder="Search formats" onChange={handleChange} value={searchTerm} />
        {searchTerm && (
          <Button variant="outline-secondary" onClick={handleClear}>
            X
          </Button>
        )}
      </InputGroup>
    </Form>
  );
};

export default SimpleSearchFrom;
