export default function BigTradesTable({ trades }) {

  return (
    <div className="panel">

      <h2>Large Trades</h2>

      <table>

        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Size</th>
            <th>Value</th>
          </tr>
        </thead>

        <tbody>

          {trades.map((t, idx) => (

            <tr key={idx}>

              <td>{t.symbol}</td>

              <td>${Number(t.price).toFixed(2)}</td>

              <td>{t.size}</td>

              <td>
                ${Number(t.value).toLocaleString()}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}
