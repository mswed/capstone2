import { useState } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';

/**
 * A search form component that filters the results provided by the parent
 * copmonent. The compoennt shows the UI AND filters the results, using the parent's
 * setState function to apply the search
 *
 * @param {Array} fields - The fields to search
 * @param {Array} targetArray - The array to filter
 * @param {Array} setTargetArray - The parents setState function used to apply the search in the parent
 * @param {Array} originalArray - A copy of the targetArray's initial state used to restore the results when needed
 * @returns {Component} - A search field and a clear button
 */

const LocalSearchForm = ({ fields, targetArray, setTargetArray, originalArray }) => {
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

export default LocalSearchForm;
