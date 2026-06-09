export default function TopFlowTable({ rows }) {

  return (
    <div className="panel">

      <h2>Top Money Flow</h2>

      <table>

        <thead>
          <tr>
            <th>Symbol</th>
            <th>Score</th>
            <th>Money Flow</th>
          </tr>
        </thead>

        <tbody>

          {rows.map((r, idx) => (

            <tr key={idx}>

              <td>{r.symbol}</td>

              <td>{r.score}</td>

              <td>
                ${Number(r.money_flow).toLocaleString()}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}
