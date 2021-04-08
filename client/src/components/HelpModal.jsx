const HELPTEXT = `
TODO: add some helpful text

Coordinate input box format: lat-decimal, lon-decimal
Example: 
53.509905, -113.541233

The target distance is to be entered in kilometers
4.5 km should be entered as 4.5
500 meters should be entered as 0.5
`

const onClick =() => {
    alert(HELPTEXT);
}
const HelpModal = () => {
    return <button onClick={onClick}> Want help? </button>
}

export default HelpModal