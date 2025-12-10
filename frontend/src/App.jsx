import React, {useState, useEffect} from "react";
import ToolList from "./pages/ToolList";
import ToolForm from "./pages/ToolForm";
import { fetchCategories } from "./api";

export default function App(){
  const [category, setCategory] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <header className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold">Inventaire Outils</h1>
        <p className="text-sm text-gray-600">Ajoute et consulte tes outils depuis mobile</p>
      </header>
      <main className="max-w-3xl mx-auto mt-4">
        <ToolForm onAdded={() => window.dispatchEvent(new Event('refresh-tools'))}/>
        <ToolList />
      </main>
    </div>
  )
}
