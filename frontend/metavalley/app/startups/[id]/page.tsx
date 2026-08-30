import CanvasSection from "@/app/components/CanvasSection";
import ProductsSection from "@/app/components/ProductsSection";


export default async function StartupPanelPage({ params }: PageProps<"/startups/[id]">) {
  const { id } = await params;

  return (
    <div>
      <CanvasSection startupId={id} />
      <ProductsSection startupId={id} />
    </div>
  );
}

