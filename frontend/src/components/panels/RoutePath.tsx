type RoutePathProps = {
  route: string[];
  selectedHop?: string;
};

export default function RoutePath({ route, selectedHop }: RoutePathProps) {
  return (
    <div className="route-path" aria-label="Route path">
      {route.map((hub, index) => (
        <span className="route-path__item" key={hub}>
          <span className={hub === selectedHop ? 'is-selected' : ''}>{hub}</span>
          {index < route.length - 1 ? <i aria-hidden="true" /> : null}
        </span>
      ))}
    </div>
  );
}
