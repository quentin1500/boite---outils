import React, {useState, useEffect} from "react";
import { fetchTools } from "../api";

export default function ToolList(){
  const [tools, setTools] = useState([]);
  const [q, setQ] = useState("");

  async function load(){
    const res = await fetchTools({ q });
    setTools(res);
  }

  useEffect(()=>{
    load();
    const handler = () => load();
    window.addEventListener("refresh-tools", handler);
    return ()=> window.removeEventListener("refresh-tools", handler);
  }, [q]);

  return (
    <div className="bg-white p-4 rounded shadow">
      <div className="flex mb-3">
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Recherche par nom..." className="flex-1 border p-2 rounded" />
        <button onClick={load} className="ml-2 px-3 py-2 bg-gray-200 rounded">Rechercher</button>
      </div>

      <ul>
        {tools.length === 0 && <li className="text-sm text-gray-500">Aucun outil</li>}
        {tools.map(t => (
          <li key={t.id} className="border-b py-2 flex justify-between items-center">
            <div>
              <div className="font-medium">{t.name}</div>
              <div className="text-sm text-gray-600">{t.description}</div>
              <div className="text-xs mt-1">{t.tags?.join(", ")}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
