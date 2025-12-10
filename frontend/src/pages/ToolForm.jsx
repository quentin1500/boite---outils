import React, {useState} from "react";
import { createTool, fetchTags } from "../api";

export default function ToolForm({ onAdded }){
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");

  async function submit(e){
    e.preventDefault();
    const tag_list = tags.split(",").map(t => t.trim()).filter(Boolean);
    await createTool({ name, description, tag_names: tag_list });
    setName(""); setDescription(""); setTags("");
    if(onAdded) onAdded();
    window.dispatchEvent(new Event('refresh-tools'));
  }

  return (
    <form onSubmit={submit} className="bg-white p-4 rounded shadow mb-4">
      <div className="mb-2">
        <label className="block text-sm font-medium">Nom</label>
        <input value={name} onChange={e=>setName(e.target.value)} required className="w-full border p-2 rounded" />
      </div>
      <div className="mb-2">
        <label className="block text-sm font-medium">Description</label>
        <input value={description} onChange={e=>setDescription(e.target.value)} className="w-full border p-2 rounded" />
      </div>
      <div className="mb-2">
        <label className="block text-sm font-medium">Tags (séparés par ,)</label>
        <input value={tags} onChange={e=>setTags(e.target.value)} className="w-full border p-2 rounded" />
      </div>
      <div className="flex justify-end">
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Ajouter</button>
      </div>
    </form>
  )
}
